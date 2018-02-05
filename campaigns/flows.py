from yoflow import flow
from campaigns import models, utils


class CampaignFlow(flow.Flow):
    model = models.Campaign
    states = dict(model.STATES)
    transitions = {
        model.DRAFT: [model.PENDING],
        model.PENDING: [model.REJECTED, model.APPROVED],
        model.REJECTED: [model.PENDING, model.APPROVED],
        model.APPROVED: [model.DELETED],
        model.DELETED: [],
    }
    KEY_COMMENT = 'comment'

    def update(self, obj, json, request):
        obj.json = json
        obj.name = json['setup']['name']['value']
        obj.start = json['setup']['start']['value']
        obj.end = json['setup']['end']['value']
        obj.retailer = int(json['retailer'])
        obj.type = int(json['type'])
        obj.owner = request.user if request.user.is_anonymous is not True else None         # TODO make this required

    def create(self, obj, json, request, **kwargs):
        self.update(obj=obj, json=json, request=request)

    def on_draft(self, request, obj, json, **kwargs):
        self.update(obj=obj, json=json, request=request)

    def on_pending(self, obj, state_changed, **kwargs):
        if state_changed:
            utils.send_pending_email(campaign=obj)

    def on_rejected(self, json, meta, state_changed, **kwargs):
        if state_changed:
            comment = json[self.KEY_COMMENT] if json else None
            if comment:
                meta[self.KEY_COMMENT] = json[self.KEY_COMMENT]
            utils.send_rejection_email(campaign=obj, comment=comment)

    def on_approved(self, obj, meta, json, state_changed, **kwargs):
        if state_changed:
            comment = json[self.KEY_COMMENT] if json else None
            if comment:
                meta[self.KEY_COMMENT] = json[self.KEY_COMMENT]
            utils.create_campaign(campaign=obj)
            utils.send_approval_email(campaign=obj, comment=comment)

    def on_deleted(self, obj, **kwargs):
        utils.cancel_campaign(campaign=obj)
        utils.send_deleted_email(campaign=obj)

    def authenticate(self, request):
        # TODO validate user has access to retailer
        pass
