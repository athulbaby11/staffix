"""Management command to back up the SQLite database (and optionally media files).

Usage:
    python manage.py backup_db
    python manage.py backup_db --include-media

Designed to be run on a schedule (e.g. every 8 hours) via Windows Task
Scheduler or a Linux cron job / systemd timer. Old backups beyond
settings.BACKUP_RETENTION_COUNT are automatically deleted.
"""
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a timestamped backup of the database (and optionally media files), pruning old backups.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--include-media',
            action='store_true',
            help='Also archive the media/ folder (uploaded documents/photos) alongside the database backup.',
        )

    def handle(self, *args, **options):
        db_settings = settings.DATABASES['default']
        if db_settings['ENGINE'] != 'django.db.backends.sqlite3':
            self.stderr.write(self.style.ERROR(
                'backup_db currently only supports the sqlite3 backend used by this project.'
            ))
            return

        db_path = Path(db_settings['NAME'])
        if not db_path.exists():
            self.stderr.write(self.style.ERROR(f'Database file not found: {db_path}'))
            return

        backup_dir = Path(settings.BACKUP_DIR)
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        db_backup_path = backup_dir / f'db_backup_{timestamp}.sqlite3'

        # Use SQLite's own backup API so we get a consistent copy even if the
        # database is being written to at the same time.
        source = sqlite3.connect(str(db_path))
        try:
            dest = sqlite3.connect(str(db_backup_path))
            try:
                source.backup(dest)
            finally:
                dest.close()
        finally:
            source.close()

        self.stdout.write(self.style.SUCCESS(f'Database backed up to {db_backup_path}'))

        if options['include_media']:
            media_root = Path(settings.MEDIA_ROOT)
            if media_root.exists():
                media_archive_base = backup_dir / f'media_backup_{timestamp}'
                archive_path = shutil.make_archive(str(media_archive_base), 'zip', root_dir=str(media_root))
                self.stdout.write(self.style.SUCCESS(f'Media files backed up to {archive_path}'))
            else:
                self.stdout.write(self.style.WARNING(f'Media root not found, skipping: {media_root}'))

        self._prune_old_backups(backup_dir)

    def _prune_old_backups(self, backup_dir):
        """Keep only the most recent BACKUP_RETENTION_COUNT backups of each type."""
        retention = settings.BACKUP_RETENTION_COUNT
        for pattern in ('db_backup_*.sqlite3', 'media_backup_*.zip'):
            files = sorted(backup_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
            for old_file in files[retention:]:
                old_file.unlink()
                self.stdout.write(f'Removed old backup: {old_file.name}')
