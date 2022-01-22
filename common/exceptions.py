# -*- coding: utf-8 -*-
import logging


class BaseException(Exception):
    message = "An unknown exception occurred."
    code = 500

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if "code" not in self.kwargs and hasattr(self, "code"):
            self.kwargs["code"] = self.code

        if message:
            self.message = message

        try:
            self.message = self.message % kwargs
        except Exception as e:
            # kwargs doesn't match a variable in the message
            # log the issue and the kwargs
            logging.exception(
                "Exception in string format operation, kwargs: %s", self.message
            )
            raise e

        super(BaseException, self).__init__()

    def __str__(self):
        return self.message


class NotFound(BaseException):
    message = "Resource could not be found."
    code = 404


class AccessForbidden(BaseException):
    message = "Access Forbidden"
    code = 403


class Unauthorized(BaseException):
    message = "Not Authorized"
    code = 401


class Conflict(BaseException):
    message = "Conflict."
    code = 409


class TableCreateError(BaseException):
    message = "Table Create Error"
    code = 1001


class AccountNotFound(NotFound):
    message = "Account with ID %(account_id)s not found"


class AccountNameNotFound(NotFound):
    message = "Account with Name %(account_name)s not found"


class AccountCreateError(TableCreateError):
    message = "Account with Name %(account_name)s create fail"


class AssetNotFound(NotFound):
    message = "Asset with ID %(asset_id)s not found"


class AssetNameNotFound(NotFound):
    message = "Asset with Name %(asset_name)s not found"


class SymbolNotFound(NotFound):
    message = "Symbol with ID %(symbol_id)s not found"


class SymbolNameNotFound(NotFound):
    message = "Symbol with Name %(symbol_name)s not found"


class ExchangeNotFound(NotFound):
    message = "Exchange with ID %(exchange_id)s not found"


class OrderNotFound(NotFound):
    message = "Order with ID %(order_id)s not found"


class AccountNameAlreadyExists(Conflict):
    message = "Account with Name %(account_name)s already exists"


class AssetNameAlreadyExists(Conflict):
    message = "Asset with Name %(asset_name)s already exists"


class SymbolNameAlreadyExists(Conflict):
    message = "Symbol with Name %(symbol_name)s already exists"


class ExchangeNameAlreadyExists(Conflict):
    message = "Exchange with Name %(exchange_name)s already exists"


class OrderAlreadyExists(Conflict):
    message = "Order with request_id %(request_id)s already exists"


class ParamError(BaseException):
    message = "illegal param"
    code = 400


class MethodFailure(BaseException):
    message = "server constraint"
    code = 420
