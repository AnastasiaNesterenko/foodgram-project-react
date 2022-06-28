from django.core.exceptions import PermissionDenied


class UpdateModelCustom:
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'У вас недостаточно прав '
                'для выполнения данного действия.'
            )
        super().perform_update(serializer)


class DestroyModelCustom:
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'У вас недостаточно прав '
                'для выполнения данного действия.'
            )
        super().perform_destroy(instance)


class CustomModel(UpdateModelCustom, DestroyModelCustom):
    pass
