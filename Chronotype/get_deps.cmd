mkdir downloaded
cd downloaded

git clone --depth=1 https://github.com/django-nonrel/django.git
move django\django ..

git clone --depth=1 https://github.com/django-nonrel/djangoappengine.git
move djangoappengine\djangoappengine ..

git clone --depth=1 https://github.com/django-nonrel/djangotoolbox.git
move djangotoolbox\djangotoolbox ..

hg clone https://bitbucket.org/twanschik/django-autoload
move django-autoload\autoload ..

git clone --depth=1 https://github.com/django-nonrel/django-dbindexer.git
move django-dbindexer\dbindexer ..

