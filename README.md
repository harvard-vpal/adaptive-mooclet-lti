# Qualtrics LTI Bridge

## Introduction

### Description
Django/Python implementation of Qualtrics LTI Bridge (Joseph Jay Williams and Sam Maldonaldo) and Adaptive Quiz Engine (Jacob Whitehill). Django LTI functionality from [bootstrap_lti_django](https://github.com/penzance/bootstrap_lti_django) LTI Django template.

### Requirements
External libraries used include
* [django-auth-lti](https://github.com/Harvard-University-iCommons/django-auth-lti)
* [ims-lti-py](https://github.com/harvard-dce/dce_lti_py)
* [dce-lti-py](https://github.com/harvard-dce/dce_lti_py) (A fork of [ims-lti-py](https://github.com/tophatmonocle/ims_lti_py))
* [django-sslserver](https://github.com/teddziuba/django-sslserver)


## Setup

### Downloading the repository and installing requirements
```
# download repo
git clone https://github.com/kunanit/qualtrics-lti-bridge.git
# (optional) create virtual environment
# install requirements
pip install -r requirements_local.txt --upgrade

# try removing the "--upgrade" option if you're using a conda environment and get a setuptools related error
```

### Edit secure.py

You must edit `secure.py` before deploying your application. The file `secure.py.example` can be used as a template. If you do not have a `django_secret_key`, you can start a new django project to obtain one.

Remember the key and value you choose for `lti_oauth_credentials`; you will need this when installing the tool in Canvas.

secure.py.example
```
SECURE_SETTINGS = {

	# required for Django
	'django_secret_key': 'changeme,',

	# required for LTI
	'lti_oauth_credentials': {
		'key': 'value',
	},
}
```

### Initialize project
```
python manage.py migrate
# (optional: create superuser)
python manage.py collectstatic
python manage.py runsslserver 0.0.0.0:8000
```
Now open a browser and enter:
`https://localhost:8000/qlb/tool_config`
Your browser will likely block you from viewing this page. You must override this.
![Chrome Security Warning](/images/chrome_error.png)

Copy all the XML data; you will need this to install your tool in Canvas.

Resources on LTI XML configuration:
* [XML config builder](https://www.edu-apps.org/build_xml.html)
* [XML config examples](https://canvas.instructure.com/doc/api/file.tools_xml.html)

### Install tool on Canvas
Navigate to the settings page of the COURSE you would like to install the tool for. (Note that this settings page can be found on the left sidebar of the course page. This is different from the settings page found in the upper right toolbar.)
![Add tool to Canvas 1](/images/add_app_canvas.png)

Click the "Add New App" button.
You may choose any name for the tool. Consumer Key and Shared Secret must be the key and value you choose for `lti_oauth_credentials` in `secure.py`. Configuration type should be Paste XML. In the following text box, paste the XML that was generated at `https://localhost:8000/lti_tools/basic_lti_app/tool_config`

![Add tool to Canvas 2](/images/add_app_canvas_2.png)
