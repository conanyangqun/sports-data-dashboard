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
    error_count = 0
    
    for fit_file in fit_files:
        try:
            parser = FITParser(fit_file)
            
            if not parser.validate():
                click.echo(f'Invalid FIT file: {fit_file}')
                error_count += 1
                continue
            
            activity_data = parser.parse()
            
            if not activity_data['start_time']:
                click.echo(f'No start time found in {fit_file}')
                error_count += 1
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
            error_count += 1
    
    click.echo(f'\nImport complete: {imported_count} imported, {skipped_count} skipped, {error_count} errors')

@cli.command()
@click.option('--input', default=None, help='Database input path')
@click.option('--output', default=None, help='JSON output path')
@click.option('--minify', is_flag=True, help='Minify JSON output')
def export(input, output, minify):
    db_path = input or DATABASE_FILE
    exporter = DataExporter(db_path, output)
    data = exporter.export_to_json(pretty=not minify)
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

@cli.command(name='validate')
@click.option('--input', default=None, help='Database input path')
def validate(input):
    db_path = input or DATABASE_FILE
    exporter = DataExporter(db_path)
    result = exporter.validate_data()
    
    click.echo('\n=== Data Validation ===')
    click.echo(f'Valid: {result["valid"]}')
    click.echo(f'Activities: {result["activity_count"]}')
    click.echo(f'Users: {result["user_count"]}')
    
    if result['issues']:
        click.echo('\nIssues:')
        for issue in result['issues']:
            click.echo(f'  - {issue}')
    else:
        click.echo('No issues found')

@cli.group()
def user():
    pass

@user.command()
@click.argument('username')
@click.option('--display-name', default=None, help='Display name')
@click.option('--avatar', default=None, help='Avatar URL')
@click.option('--bio', default=None, help='User bio')
@click.option('--output', default=None, help='Database output path')
def init(username, display_name, avatar, bio, output):
    db_path = output or DATABASE_FILE
    db = Database(db_path)
    
    user_id = db.insert_user(username, display_name, avatar, bio)
    click.echo(f'User initialized: {username} (ID: {user_id})')
    if display_name:
        click.echo(f'  Display Name: {display_name}')
    if avatar:
        click.echo(f'  Avatar: {avatar}')
    if bio:
        click.echo(f'  Bio: {bio}')

@user.command()
@click.argument('username')
@click.option('--display-name', default=None, help='Display name')
@click.option('--avatar', default=None, help='Avatar URL')
@click.option('--bio', default=None, help='User bio')
@click.option('--output', default=None, help='Database output path')
def update(username, display_name, avatar, bio, output):
    db_path = output or DATABASE_FILE
    db = Database(db_path)
    
    if not display_name and not avatar and not bio:
        click.echo('Please provide at least --display-name, --avatar or --bio option')
        return
    
    db.update_user(username, display_name, avatar, bio)
    click.echo(f'User updated: {username}')
    if display_name:
        click.echo(f'  Display Name: {display_name}')
    if avatar:
        click.echo(f'  Avatar: {avatar}')
    if bio:
        click.echo(f'  Bio: {bio}')

@user.command()
@click.option('--output', default=None, help='Database input path')
def delete(output):
    db_path = output or DATABASE_FILE
    db = Database(db_path)
    
    user = db.get_user()
    if not user:
        click.echo('No user found in database')
        return
    
    if click.confirm(f'Are you sure you want to delete user "{user["username"]}"?'):
        db.delete_user()
        click.echo('User deleted successfully')

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
        click.echo(f'Display Name: {user["display_name"] or "Not set"}')
        click.echo(f'Avatar: {user["avatar_url"] or "Not set"}')
        click.echo(f'Bio: {user["bio"] or "Not set"}')
    else:
        click.echo('No user found in database')

@cli.group()
def activity():
    pass

@activity.command()
@click.argument('activity_id', type=int)
@click.option('--input', default=None, help='Database input path')
def delete(activity_id, input):
    db_path = input or DATABASE_FILE
    db = Database(db_path)
    
    activity = db.get_activity_by_id(activity_id)
    if not activity:
        click.echo(f'Activity with ID {activity_id} not found')
        return
    
    if click.confirm(f'Are you sure you want to delete activity {activity_id} ({activity["activity_type"]} on {activity["start_time"]})?'):
        db.delete_activity(activity_id)
        click.echo('Activity deleted successfully')

@activity.command()
@click.option('--start-date', required=True, help='Start date (YYYY-MM-DD)')
@click.option('--end-date', required=True, help='End date (YYYY-MM-DD)')
@click.option('--input', default=None, help='Database input path')
@click.option('--confirm', is_flag=True, help='Skip confirmation prompt')
def delete_range(start_date, end_date, input, confirm):
    db_path = input or DATABASE_FILE
    db = Database(db_path)
    
    activities = db.get_activities_by_date_range(start_date, end_date)
    
    if not activities:
        click.echo(f'No activities found between {start_date} and {end_date}')
        return
    
    click.echo(f'Found {len(activities)} activities in the date range:')
    for activity in activities:
        click.echo(f'  - ID {activity["id"]}: {activity["activity_type"]} on {activity["start_time"]}')
    
    if confirm or click.confirm(f'\nAre you sure you want to delete {len(activities)} activities?'):
        deleted_count = db.delete_activities_by_date_range(start_date, end_date)
        click.echo(f'{deleted_count} activities deleted successfully')
    else:
        click.echo('Deletion cancelled')

@activity.command()
@click.argument('activity_id', type=int)
@click.option('--input', default=None, help='Database input path')
def show(activity_id, input):
    db_path = input or DATABASE_FILE
    db = Database(db_path)
    
    activity = db.get_activity_by_id(activity_id)
    
    if not activity:
        click.echo(f'Activity with ID {activity_id} not found')
        return
    
    click.echo('\n=== Activity Details ===')
    click.echo(f'ID: {activity["id"]}')
    click.echo(f'Type: {activity["activity_type"]}')
    click.echo(f'Start Time: {activity["start_time"]}')
    click.echo(f'Duration: {activity["duration"]:.2f} seconds')
    click.echo(f'Distance: {activity["distance"]:.2f} meters')
    click.echo(f'Calories: {activity["calories"]}')
    if activity['max_speed']:
        click.echo(f'Max Speed: {activity["max_speed"]:.2f} m/s')
    if activity['avg_speed']:
        click.echo(f'Avg Speed: {activity["avg_speed"]:.2f} m/s')
    if activity['max_heart_rate']:
        click.echo(f'Max Heart Rate: {activity["max_heart_rate"]} bpm')
    if activity['avg_heart_rate']:
        click.echo(f'Avg Heart Rate: {activity["avg_heart_rate"]} bpm')
    if activity['max_cadence']:
        click.echo(f'Max Cadence: {activity["max_cadence"]} rpm')
    if activity['avg_cadence']:
        click.echo(f'Avg Cadence: {activity["avg_cadence"]} rpm')
    if activity['max_power']:
        click.echo(f'Max Power: {activity["max_power"]} W')
    if activity['avg_power']:
        click.echo(f'Avg Power: {activity["avg_power"]} W')
    if activity['normalized_power']:
        click.echo(f'Normalized Power: {activity["normalized_power"]} W')
    if activity['elevation_gain']:
        click.echo(f'Elevation Gain: {activity["elevation_gain"]} meters')

if __name__ == '__main__':
    cli()
