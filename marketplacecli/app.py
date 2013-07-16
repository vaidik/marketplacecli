"""
Marketplace CLI - to make everyday things easy to work with Marketplace.
"""


from marketplace.auth import OAuth
from marketplace.client import Client
from pyquery import PyQuery as pq

import json
import os


def create_app(client, price, categories=None):
    """Submit an app on marketplace.
    """

    # get a dummy manifest
    manifest = get_hosted_manifest()

    # validate app
    validation = client.apps.validate_app(manifest=manifest)
    assert validation.status_code == 201, ('Unable to validate app. Probably '
                                           'invalid manifest %s.' % manifest)
    validation = json.loads(validation.text)

    # submit app
    app = client.apps.create_app(manifest=validation['id'])
    assert app.status_code == 201, 'Unable to submit app to marketplace.'
    app = json.loads(app.text)

    # update app
    app['premium_type'] = 'premium'
    app['price'] = price
    app['support_email'] = 'test@mozilla.com'
    app['device_types'] = ['firefoxos']
    app['categories'] = categories or [157, 158]
    app['regions'] = ['es']
    response = client.apps.update_app(app['id'], app)
    assert response.status_code == 202, 'Unable to update app details.'

    # upload a dummy valid screenshot
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'image.png')
    preview = client.apps.add_preview(app['id'], 1, image_path, 'image/png')
    assert preview.status_code == 201, 'Unable to upload screenshot.'

    # change status to put in review queue
    resp = client.apps.change_app_status(app['id'], 'pending')
    assert resp.status_code == 202, 'Unable to change status to *pending*.'

    return app


def get_hosted_manifest():
    """Get URL of a test (dummy) hosted app's manifest.
    """

    dollar = pq(url='http://testmanifest.com/')
    return dollar('#thingy').val()


def get_tiers(client):
    """Get payment tiers.
    """

    tiers = client.payments.get_tiers()
    assert tiers.status_code == 200, ('Unable to get Payment Tiers from '
                                      'marketplace.')

    tiers = json.loads(tiers.text)
    return tiers['objects']
