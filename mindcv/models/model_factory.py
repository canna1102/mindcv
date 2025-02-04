from .registry import is_model, model_entrypoint
from mindspore import load_checkpoint, load_param_into_net


def create_model(
        model_name: str,
        num_classes: int = 1000,
        pretrained=False,
        in_channels: int = 3,
        checkpoint_path: str = '',
        **kwargs):

    if checkpoint_path != '' and pretrained:
        raise ValueError('checkpoint_path is mutually exclusive with pretrained')

    model_args = dict(num_classes=num_classes, pretrained=pretrained, in_channels=in_channels)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    if not is_model(model_name):
        raise RuntimeError('Unknown model (%s)' % model_name)

    create_fn = model_entrypoint(model_name)
    model = create_fn(**model_args, **kwargs)

    if checkpoint_path:
        param_dict = load_checkpoint(checkpoint_path)
        load_param_into_net(model, param_dict)

    return model
