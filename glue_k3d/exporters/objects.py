from glue.config import DictRegistry


class K3DLayerObjectsRegistry(DictRegistry):

    def add(self, layer_cls, object_creator):
        self.members[layer_cls] = object_creator

    def __call__(self, layer_cls):
        def adder(object_creator):
            self.add(layer_cls, object_creator)
            return object_creator
        return adder


k3d_layer_object = K3DLayerObjectsRegistry()
