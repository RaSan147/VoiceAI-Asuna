__all__ = { 'os_name',}


from platform import system as os_name
os_name = os_name()