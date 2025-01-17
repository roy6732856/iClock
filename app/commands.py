import click
from flask.cli import with_appcontext
from app.models.company import Company
from app.utils.database import db

@click.command('create-company')
@click.argument('name')
@click.argument('code')
@with_appcontext
def create_company(name, code):
    """創建新公司"""
    company = Company(name=name, code=code)
    db.session.add(company)
    db.session.commit()
    click.echo(f'Created company {name} with code {code}') 