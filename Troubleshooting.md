# Troubleshooting

Here are some error I faced while working with odoo and what worked for me.

Make sure you are on ?debug=assets mode


## The style compilation failed, see the error below. Your recent actions may be the cause, please try reverting the changes you made.

This error happened to me when I edited assets (scss and js) from the web editor.

```
The style compilation failed, see the error below. Your recent actions may be the cause, please try reverting the changes you made.

Could not get content for /website/static/src/scss/options/user_values.custom.web.assets_common.scss defined in bundle 'web.assets_common'.
Could not get content for /website/static/src/scss/options/colors/user_color_palette.custom.web.assets_common.scss defined in bundle 'web.assets_common'.
Could not get content for /website/static/src/scss/options/colors/user_theme_color_palette.custom.web.assets_common.scss defined in bundle 'web.assets_common'.
```

You have these original files on the folder, but they are not touched.

Whenever you edit the assets from the web editor, odoo creates:
- A version of the file on the database (you'll find it in filestore folder)
- A view for the the version

If you erase the filestore, you lose it and the error appears.

### Solution

From Apps Home:

- Click on Settings
- At the topbar menu:
  -  Technical
    -  User Interface > Views

On Views:

Add custom filter:
- Arch Filename
- is not set
Apply

You now may see the QWeb views for these files.

Select and delete all '/website/static/src/scss/options/user_\[filename\]' rows 
