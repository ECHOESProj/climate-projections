from app.climate_projections import climate_projections
import logging
from app.init import get_env, get_path
#import click
# @click.command(context_settings=dict(
#      ignore_unknown_options=True,
#      allow_extra_args=True
# ))
# def cli(module):
#     climate_projections()
        
if __name__ == "__main__":
    climate_projections()
