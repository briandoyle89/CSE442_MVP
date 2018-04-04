from django.apps import AppConfig

#Althogh generally each component is an app itself. But for this the main functioning MVP  is just one app. 
class ProjectConfig(AppConfig):
    name = 'project'
