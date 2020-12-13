# Gecolsa - Website

Gecolsa CMS. Has a merchandise virtual
shop, integration with http://cat-ebusiness.com/cpc and navigation according
to Gecolsa needs. Gets user navigation habits.

# Docker

We are using Docker to isolate the development environment to have a single
and stable operating system and libraries.

## Installation

With docker and docker-compose installed run:

    $ test ! -e app/local_settings.py && cp app/.local_settings.py app/local_settings.py

This will copy a base local_settings.py file if you don't have any and it will
build the docker images required to run the project, this will take some minutes
but is only needed once.


## Running

To run or update your local environment you can run:

    $ docker-compose up

It will rebuild you image, since Docker has a cache mechanism it will take
less than building the image for the first time.


## Database

Since Docker does not come with database contents you migth need to populate
your database first, you can do that by restoring a database from a file:

    $ docker-compose exec mdillon__postgis bash -c 'psql --dbname=postgres --username=postgres --command="DROP SCHEMA public CASCADE;CREATE SCHEMA public;" && pg_restore /tmp/data/db.dump --dbname=postgres --username=postgres --no-owner'

If a db.dump file is in the root directory of your project it will work and load
that file into the database used by Docker. You can do this anytime you need.

You can connect to the database shell using:

    $ docker-compose exec mdillon__postgis psql --dbname=postgres --username=postgres


## Commands

Running gulp to have livereload on templates and frontend files:

    $ docker-compose exec web gulp

> At this time running gulp is very slow.

To run any command on the app container you must do:

    $ docker-compose exec web python manage.py createsuperuser
    $ docker-compose exec web python manage.py shell_plus
    $ docker-compose exec web python manage.py test --failfast --parallel
    $ docker-compose exec web bash

Running celery:

    $ docker-compose exec web ./bin/celery-worker

To regenerate search index for search results:

    $ docker-compose exec web python manage.py rebuild_index


### Celery Tasks

To run them in your local, apply:

    $ ./manage.py celery worker --loglevel=info


### Woosh Search

Make sure you have your index created

    $ ./manage.py rebuild_index


## Shopping cart

A cookie is used to store the temporary products chosen by the user, the
structure is::

    {
        'products': [{
            'reference':,
            'product_stock': {
                'quantity',
                'size_id'
            },
        }],
    }

## Inventory Updating

We provided a sample for consuming our webservice in C#, it can be found in
doc/source/update_inventory.cs , you need to install mono in OS/X or Linux
in order to test it.

To compile::

    mcs /reference:System.Web.Extensions update_inventory.cs

To execute::

    mono update_inventory.exe


## Caterpillar Webservice Integration

We used the `suds` library to query the Cat WSs, a nightly process with the
SalesChannelCode provided by Gecolsa.

* [Nightly Batch Process](http://cat-ebusiness.com/cpc/developers/nightly-batch-process/)
* [WSDL](https://cpc.cat.com/ws/services/XmlUpdate?wsdl)
* [View Category Info](https://cpc.cat.com/ws/xml/es/324/324_es.xml)
* [View Product Info](https://cpc.cat.com/ws/xml/es/324/18255128_es.xml)
* [Sample](http://www.cat.com/en_US/products/new/equipment/wheel-loaders/large-wheel-loaders/18568699.html)
* [Schema Documentation](http://cat-ebusiness.com/cpc/xsd/docs/index.html#getClasses)
* [Equipment Example](http://cat-ebusiness.com/cpc/developers/example-xml-files/example-equipment-xml-gis/)

The approach is to download the classes specified and from there the Tree of
groups and the actual products provided by Caterpillar.

There are two ways to refresh the contents of the website:

1. Nightly builds: At 2:00AM the website is refreshed
2. Button from the admin: A task that sends an OK when finished

The process consists of:

1. Get all the possible groups and products with last_update timestamp
2. Update all the products that had a newer timestamp than that of stored
   previously, put the html data directly in the description field. The images
   are taken from the ws and served by us on the size specification.
3. If there are new products they are reported to the configured emails.


## Work on multiple products from xml

If you have to do tasks for many products using information from the CAT Ws you
can create a function to work on a single product and pass as a parameter to
the `apply_to_many` function present in `product/tasks.py`

Here is an example:

    from product.tasks import apply_to_many, load_other_images
    product_list = Equipment.objects.filter(id__in=[...])
    apply_to_many(product_list, load_other_images, verbosity=True)

Your function must receive an instance of Caterpillar Fetcher and the xml-id
of the product to be operated on.  The function must return a counter and a
list of errors if any.


## Testing virtual shop

You can get the credential testing for Payu via http://desarrolladores.payulatam.com/webcheckout-integracion/ use 9955555555555501 VISA credit card.


## Upgrade packages

To upgrade packages version run:

    $ docker-compose exec web yarn outdated
    $ docker-compose exec web piprot --latest --verbatim
    $ ./update-docker-image.sh

## Provisioning infrastructure

For the production environment we have an automated script that takes care
of provisioning a production server. For doing this provisioning on your own
you must have ansible installed in your local machine.

    $ pip install ansible

Then you must create a hosts file.

    $ sudo mkdir /etc/ansible
    $ sudo vim /etc/ansible/hosts

In the ```hosts``` file add the next lines:

    [gecolsa]
    <ip>    bitbucket_user=<username>     bitbucket_pass=<password>

> Replace each <var> accordingly

Run:

    $ ansible-playbook playbook-server.yml

# Database Models
![alt text](https://gecolsa.com/uploads/static_pictures/gecolsa-dbmodel.png "Gecolsa db model")

