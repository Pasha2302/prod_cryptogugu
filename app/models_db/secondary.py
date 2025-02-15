from django.utils.text import slugify


def save_slug(self, _super, additionally=None, *args, **kwargs):
    if additionally is None: additionally = ''
    if not self.slug: self.slug = slugify(f"{self.name} {additionally}".strip())
    _super.save(*args, **kwargs)

