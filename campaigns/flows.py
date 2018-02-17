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

    @staticmethod
    def update(obj, json, request):
        obj.json = json
        obj.name = json['setup']['name']['value']
        obj.start = json['setup']['start']['value']
        obj.end = json['setup']['end']['value']
        obj.retailer = int(json['retailer'])
        obj.type = int(json['type'])
        obj.owner = request.user if request.user.is_anonymous is not True else None  # TODO make this required

    @staticmethod
    def create(obj, json, request, **kwargs):
        self.update(obj=obj, json=json, request=request)

    @staticmethod
    def on_draft(request, obj, json, **kwargs):
        self.update(obj=obj, json=json, request=request)

    @staticmethod
    def on_pending(obj, state_changed, **kwargs):
        if state_changed:
            utils.send_pending_email(campaign=obj)

    @staticmethod
    def on_rejected(json, meta, state_changed, **kwargs):
        if state_changed:
            comment = json[self.KEY_COMMENT] if json else None
            if comment:
                meta[self.KEY_COMMENT] = json[self.KEY_COMMENT]
            utils.send_rejection_email(campaign=obj, comment=comment)

    @staticmethod
    def on_approved(obj, meta, json, state_changed, **kwargs):
        if state_changed:
            comment = json[self.KEY_COMMENT] if json else None
            if comment:
                meta[self.KEY_COMMENT] = json[self.KEY_COMMENT]
            utils.create_campaign(campaign=obj)
            utils.send_approval_email(campaign=obj, comment=comment)

    @staticmethod
    def on_deleted(obj, **kwargs):
        utils.cancel_campaign(campaign=obj)
        utils.send_deleted_email(campaign=obj)
