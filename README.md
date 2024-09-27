# ODmapper - Omics Data Mapping and Harmonizer
ODmapper is used to map a genomic variant to the OMOP concept_id (particularly OMOP Genomic) through API call based on Django REST framework.
In a nutshell, a user can use the API to query the "CONCEPT" and "CONCEPT_SYNONYM" of OMOP CDM tables based on the query text (concept_id, concept_synonym, concept_name and concept_code).

To set up ODmapper, the user needs to:
1. Set up the OMOP CDM database
2. Install and configure Django REST Framework (DRF)

## Set up the OMOP CDM database
Please refer to [Common Data Model](https://github.com/OHDSI/CommonDataModel/) for the set up of OMOP CDM database.

#### The Genomic Vocabulary in OMOP CDM
Two sources of genomic vocabulary are used:
1. The OMOP Genomic vocabulary which can be downloaded from [ATHENA](https://athena.ohdsi.org/vocabulary/list).
2. The additional genomic vocabulary which is potentially clinically relevant, we have added together with this package as [enriched-vocab.tar.gz](./enriched-vocab.tar.gz). The additional vocabulary are obtained from:
    - [ClinGen Resource](https://search.clinicalgenome.org/kb/downloads) which includes variants in Gene-Disease validity as well as Variant Pathogenicity.
    - [SG10K Health Study](https://pubmed.ncbi.nlm.nih.gov/36335097/)

## Setup Django REST Framework
Let's clone the repository:
```
git clone https://github.com/biierwint/ODmapper.git
```
Navigate to folder "ODmapper"
```
cd ODmapper/
```
Create virtual environment
```
python3 -m venv odmapperenv
```
Activate virtual environment
```
source odmapperenv/bin/activate
```
Install packages
```
pip install -r requirements.txt
```

#### Create project "odmapper_api" and app "odmapper"
Create project
```
django-admin startproject odmapper_api
```
Change directory to "odmapper_api"
```
cd odmapper_api/
```
Create odmapper app
```
python manage.py startapp odmapper
```
Configure Django (odmapper_api/settings.py)
- Note: we provide settings.py.example (source/odmapper_api/settings.py.example) for reference


#### Collect static files
Please ensure that you have configure Django accordingly in the settings.py file (i.e. configure the STATIC_URL and STATIC_ROOT). If you set "DEBUG = True", then you can skip this section. Otherwise, please run collectstatic files accordingly.
```
python manage.py collectstatic
```

#### Copy source file to odmapper/ folder
Please make sure you are in the "ODmapper" folder.
Copy the files inside "source/odmapper/" to your project's app.
```
cp -R source/odmapper/* odmapper_api/odmapper/
```
Copy the files inside "source/odmapper_api/" to your project's main folder (odmapper_api/odmapper_api/)
```
cp source/odmapper_api/urls.py odmapper_api/odmapper_api/
```

#### Authentication
If you would like the API to be callable by authenticated user, you can start by creating super-user:
Change directory to project folder: odmapper_api/
```
cd odmapper_api/
python manage.py createsuperuser
```
Subsequently, please modify the file "odmapper/views.py" by **uncommenting** the section `permission_classes = [permissions.IsAuthenticated]`

#### Create initial migrations for database tables
[Note: This assumes that you have set up your OMOP CDM tables for concept and concept_synonym accordingly]
```
python manage.py makemigrations
python manage.py migrate
```
