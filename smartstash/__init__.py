__version_info__ = (0, 1, 1, None)
# software version: set last term to 'dev', 'pre', or None for final release

# Dot-connect all but the last. Last is dash-connected if not None.
__version__ = '.'.join(str(i) for i in __version_info__[:-1])
if __version_info__[-1] is not None:
    __version__ += ('-%s' % (__version_info__[-1],))


def version(request):
    return {
        'SW_VERSION': __version__
    }
