import boto3
import click

session = boto3.Session (profile_name = 'shotty')
ec2 = session.resource('ec2')

@click.command()  # para leer script como comando con argumentos
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances" # se añade al --help
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

      
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

if __name__ == '__main__':
    list_instances()