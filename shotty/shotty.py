import boto3
import click

session = boto3.Session (profile_name = 'shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """Commands for instances"""

#primer comando list, con su filtro por proyecto. En lugar de @click.command ahora es @instances.command para tener más de un posible comando que pertenece al grupo instances

@instances.command('list')  # para leer script como comando con argumentos
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances" # se añade al --help
    
    instances = filter_instances(project)
      
    for i in instances:
        tags ={ t['Key']: t['Value'] for t in i.tags or []}  # dictionary comprehension de: 
        #for t in i.tags: 
        #tags[t['Key']] = t['Value'] 
        #[] hace que si no hay ningun tag, no se devuelva una excepción NoneType que detenga el for
        print(','.join((i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')))) # en lugar de  directamente tags ya que con get, podemos poner un defaul a no project si no se devuelve tag

    return

#segundo comando stop con su filtro por proyecto
@instances.command('stop')
@click.option('--project', default=None,
    help='Only instances for project')

def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)
      
    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
    
    return

#tercer comando start con su filtro por proyecto
@instances.command('start')
@click.option('--project', default=None,
    help='Only instances for project')

def stop_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)
      
    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()
    
    return

if __name__ == '__main__':
    instances()