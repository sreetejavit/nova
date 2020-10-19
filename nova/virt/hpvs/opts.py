import itertools

from nova.virt.hpvs import conf as hpvs_conf


def list_opts():
    return [
        # Actually it should be [zvm], but for backward compatible issue,
        # we keep this into DEFAULT.
        ('DEFAULT',
         itertools.chain(
             hpvs_conf.hpvs_opts,
         )),
    ]
