platform='unknown'
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    platform='linux'
    echo 'your platform is ', $platform
    sudo apt-get install binutils libproj-dev gdal-bin
    sudo apt-get install spatialite-bin
elif [[ "$OSTYPE" == "darwin"* ]]; then
    platform='MacOSX'
    echo 'your platform is ', $platform
    brew install postgis
    brew install gdal
    brew install libgeoip
    brew install spatialite-tools
elif [[ "$OSTYPE" == "cygwin" ]]; then
    platform='cygwin'
    # POSIX compatibility layer and Linux environment emulation for Windows
else
    platform='unknown'
    echo 'your platform is ', $platform
    # Unknown.
fi

virtualenv env_tracker
source env_tracker/bin/activate
pip install -r reuqirements.txt
./manage.py migrate
./manage.py runserver 7001
./manage.py createsuperuser
