import os
import subprocess
import psycopg2
from configparser import ConfigParser

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUPS_DIR = os.path.join(ROOT_DIR, 'backups')


class RestoreDump:
    def __init__(self, keep_attachments=False, config_path=None):
        errors = []
        self.db_name = None
        db_params = get_config()
        if db_params:
            self.db_name = db_params['database']

        self.files = [f"{BACKUPS_DIR}/{f}" for f in os.listdir(f"{BACKUPS_DIR}/") if os.path.isfile(
            f"{BACKUPS_DIR}/{f}") and f.startswith(self.db_name) and not f.startswith('.') and not f.endswith('.py')]
        self.dump = max(self.files, key=os.path.getctime)
        self.keep_attachments = keep_attachments
        self.config_path = self.get_config_path(config_path)

        if not self.db_name:
            errors.append('Database name not found.')
        if not self.dump:
            errors.append('Dump name not found.')

        if not errors:
            self.restore_dump()
            self.update_db()

    def get_config_path(self, config_path):
        config_paths = [
            '~/.odoorc',
            os.path.join(ROOT_DIR, '.odoorc'),
        ]
        if config_path and os.path.exists(config_path):
            return config_path

        for path in config_paths:
            if os.path.exists(path):
                return path

    def restore_dump(self):
        commands = [
            f"""createuser rdsadmin""",
            f"""dropdb {self.db_name} --if-exists""",
            f"""createdb -O rdsadmin {self.db_name}""",
        ]

        unzip_proccess = None
        if self.dump.endswith('.zip'):
            unzip_proccess = 'unzip -p'
        if [self.dump.endswith(ext) for ext in ['.gzip', '.gz'] if self.dump.endswith(ext)]:
            unzip_proccess = 'gunzip -c'

        if unzip_proccess:
            commands.append(
                f"""{unzip_proccess} {self.dump} | psql {self.db_name}""")
        else:
            commands.append(f"""psql {self.db_name} < {self.dump}""")

        for command in commands:
            print(f'Running command: {command}')
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, shell=True)
            proc_stdout = process.communicate()[0].strip()
            print(proc_stdout)

    def update_db(self):
        queries = [
            "UPDATE ir_mail_server SET active=false",
            "UPDATE ir_module_module SET state='uninstalled' WHERE name='amazon_s3_storage'",
            "DELETE FROM ir_ui_view WHERE arch_fs ILIKE '%s3%'",
            "DELETE FROM bill_com_config",
            "DELETE FROM ir_ui_view WHERE id IN (2351,2345,2346,2360)",
        ]
        if not self.keep_attachments:
            queries.append("DELETE FROM ir_attachment")

        for query in queries:
            run_query(query, self.config_path)


def get_config():
    """ Returns parsed db params:
        {
        'database': '',
        'user': '',
        'host': '',
        'password': '',
        }
    """
    db_params = {}
    parser = ConfigParser()
    config_paths = [
        '~/.odoorc',
        os.path.join(ROOT_DIR, '.odoorc'),
    ]
    for path in config_paths:
        if os.path.exists(path):
            config_path = path

    if config_path:
        parser.read(config_path)

        if parser.has_section('options'):
            parser_params = {
                'db_name': 'database',
                'db_user': 'user',
                'db_host': 'host',
                'db_pass': 'password',
            }
            params = parser.items('options')
            for param in params:
                if param[0] in parser_params.keys():
                    db_params[parser_params[param[0]]] = param[1]

    return db_params


def run_query(query, config_path=None):
    conn = None
    db_params = get_config()

    if db_params:
        print('Connecting to database...')
        try:
            print(f'Running {query}')
            conn = psycopg2.connect(**db_params)

            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    else:
        raise Exception('Config file not found.')


def delete_assets():
    run_query("DELETE FROM ir_attachment WHERE mimetype='application/javascript' OR mimetype='text/css' OR name LIKE '%.scss%' ")


RestoreDump()
