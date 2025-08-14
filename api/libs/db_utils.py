from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from api import db
from api.utils.response_utils import error, HttpCode

def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(e)
        reason = str(e)
        return error(code=HttpCode.db_error, msg=reason)
