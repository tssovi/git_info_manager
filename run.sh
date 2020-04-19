os=""
case "$OSTYPE" in
 solaris*) os=SOLARIS ;;
 darwin*)  os=OSX ;;
 linux*)   os=LINUX ;;
 bsd*)     os=BSD ;;
 msys*)    os=WINDOWS ;;
 *)        os=unknown: $OSTYPE ;;
esac

if [[ "$os" == 'LINUX' ]]; then
   # Make a directory named venvs
   mkdir venvs
   # Install virtualenv
   pip3 install virtualenv --user
   # Install virtualenv globally
   sudo apt install virtualenv
   # Create a virtualenv named git_venv
   virtualenv -p python3 venvs/git_venv
   # Activate the created env
   source venvs/git_venv/bin/activate
elif [[ "$os" == 'WINDOWS' ]]; then
   # Make a directory named venvs
   mkdir \venvs
   # Install virtualenv
   pip install virtualenv
   pip install virtualenvwrapper-win
   # Create a virtualenv named git_venv
   virtualenv \venvs\git_venv
   # Activate the created env
   \venvs\git_venv\Scripts\activate
fi

# Clone project from git
git clone https://github.com/tssovi/git_info_manager.git

# Go to project directory
cd git_info_manager

# Copy example_env.py as env.py
cp -v git_manager/env_example.py git_manager/env.py

echo Please Provide Your Existing Database Name:
read db_name
sed -i -- "s/database_name/$db_name/g" git_manager/env.py

echo Please Provide Your Existing Database Username:
read db_user
sed -i -- "s/db_username/$db_user/g" git_manager/env.py

echo Please Provide Your Existing Database Password:
read db_pass
sed -i -- "s/db_password/$db_pass/g" git_manager/env.py

echo Please Provide Your Ngrok URL:
read ngrok_url
sed -i --  "s,your_ngrok_url,$ngrok_url,g" git_manager/env.py

# Install required packages
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations

# Migrate database
python manage.py migrate

# Run tests for this project
python manage.py test

# Run project
python manage.py runserver