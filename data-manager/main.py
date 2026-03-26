import click
import os
import glob
from database import Database
from parser import FITParser
from exporter import DataExporter
from config import DATABASE_FILE

@click.group()
def cli():
    pass

@cli.command()
@click.option('--output', default=None, help='Database output path')
def init(output):
    db_path = output or DATABASE_FILE
    db = Database(db_path)
    db.init_db()
    click.echo(f'Database initialized at {db_path}')

@cli.command(name='import')
@click.argument('fit_dir', type=click.Path(exists=True))
@click.option('--output', default=None, help='Database output path')
def import_cmd(fit_dir, output):
    db_path = output or DATABASE_FILE
    db = Database(db_path)
    
    fit_files = glob.glob(os.path.join(fit_dir, '*.fit'))
    
    if not fit_files:
        click.echo('No FIT files found in the directory')
        return
    
    imported_count = 0
    skipped_count = 0
    
    for fit_file in fit_files:
        try:
            parser = FITParser(fit_file)
            
            if not parser.validate():
                click.echo(f'Invalid FIT file: {fit_file}')
                continue
            
            activity_data = parser.parse()
            
            if not activity_data['start_time']:
                click.echo(f'No start time found in {fit_file}')
                continue
            
            if db.activity_exists(activity_data['start_time']):
                click.echo(f'Skipping duplicate activity: {fit_file}')
                skipped_count += 1
                continue
            
            db.insert_activity(activity_data)
            imported_count += 1
            click.echo(f'Imported: {fit_file}')
            
        except Exception as e:
            click.echo(f'Error importing {fit_file}: {e}')
    
    click.echo(f'\nImport complete: {imported_count} imported, {skipped_count} skipped')

@cli.command()
@click.option('--input', default=None, help='Database input path')
@click.option('--output', default=None, help='JSON output path')
def export(input, output):
    db_path = input or DATABASE_FILE
    exporter = DataExporter(db_path, output)
    data = exporter.export_to_json()
    click.echo(f'Exported {len(data["activities"])} activities to {exporter.json_path}')

@cli.command()
@click.option('--input', default=None, help='Database input path')
def stats(input):
    db_path = input or DATABASE_FILE
    db = Database(db_path)
    stats = db.get_stats()
    
    click.echo('\n=== Sports Data Statistics ===')
    click.echo(f'Total Activities: {stats["total_activities"]}')
    click.echo(f'Total Distance: {stats["total_distance"]:.2f} meters')
    click.echo(f'Total Duration: {stats["total_duration"]:.2f} seconds')
    click.echo('\nActivity Types:')
    for activity_type, count in stats['type_stats'].items():
        click.echo(f'  {activity_type}: {count}')

@cli.group()
def user():
    pass

@user.command()
@click.argument('username')
@click.option('--avatar', default=None, help='Avatar URL')
@click.option('--bio', default=None, help='User bio')
@click.option('--output', default=None, help='Database output path')
def init(username, avatar, bio, output):
    db_path = output or DATABASE_FILE
    db = Database(db_path)
    
    user_id = db.insert_user(username, avatar, bio)
    click.echo(f'User initialized: {username} (ID: {user_id})')
    if avatar:
        click.echo(f'  Avatar: {avatar}')
    if bio:
        click.echo(f'  Bio: {bio}')

@user.command()
@click.argument('username')
@click.option('--avatar', default=None, help='Avatar URL')
@click.option('--bio', default=None, help='User bio')
@click.option('--output', default=None, help='Database output path')
def update(username, avatar, bio, output):
    db_path = output or DATABASE_FILE
    db = Database(db_path)
    
    if not avatar and not bio:
        click.echo('Please provide at least --avatar or --bio option')
        return
    
    db.update_user(username, avatar, bio)
    click.echo(f'User updated: {username}')
    if avatar:
        click.echo(f'  Avatar: {avatar}')
    if bio:
        click.echo(f'  Bio: {bio}')

@user.command()
@click.argument('username', required=False)
@click.option('--output', default=None, help='Database input path')
def show(username, output):
    db_path = output or DATABASE_FILE
    db = Database(db_path)
    
    user = db.get_user(username)
    
    if user:
        click.echo('\n=== User Information ===')
        click.echo(f'ID: {user["id"]}')
        click.echo(f'Username: {user["username"]}')
        click.echo(f'Avatar: {user["avatar_url"] or "Not set"}')
        click.echo(f'Bio: {user["bio"] or "Not set"}')
    else:
        click.echo('No user found in database')

if __name__ == '__main__':
    cli()
