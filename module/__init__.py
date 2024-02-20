from viam.components.generic import Generic
from viam.resource.registry import Registry, ResourceCreatorRegistration
from .play_sound import SoundPlayer


Registry.register_resource_creator(Generic.SUBTYPE,
                                   SoundPlayer.MODEL,
                                   ResourceCreatorRegistration(SoundPlayer.new))
