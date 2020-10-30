# Reversing Django admin URLs

I always lose track of this and forget how to do it, so here it is.

**Reference**: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls

## AdminSite

Provides these basic patterns:

| Page                      | URL name               | Parameters                     |
| ------------------------- | ---------------------- | ------------------------------ |
| Index                     | `index`                |                                |
| Login                     | `login`                |                                |
| Logout                    | `logout`               |                                |
| Password change           | `password_change`      |                                |
| Password change done      | `password_change_done` |                                |
| i18n JavaScript           | `jsi18n`               |                                |
| Application index page    | `app_list`             | `app_label`                    |
| Redirect to object’s page | `view_on_site`         | `content_type_id`, `object_id` |

## ModelAdmin

Each ModelAdmin provides these additional patterns:

| Page       | URL name                                      | Parameters  |
| ---------- | --------------------------------------------- | ----------- |
| Changelist | `{{ app_label }}_{{ model_name }}_changelist` |             |
| Add        | `{{ app_label }}_{{ model_name }}_add`        |             |
| History    | `{{ app_label }}_{{ model_name }}_history`    | `object_id` |
| Delete     | `{{ app_label }}_{{ model_name }}_delete`     | `object_id` |
| Change     | `{{ app_label }}_{{ model_name }}_change`     | `object_id` |

### Example

Suppose you have app `whatsthisappthing` with model `IHaveNoIdeaModel`, and wish to access the **Change** view of a model instance with ID `4`. Prefix the URL pattern with `admin:`, then supply the necessary components as described above (remember to convert a model from `CamelCase` to `lowercase_with_underscores`, adding `_` between CamelCase words):

```python
from django.urls import reverse

reverse("admin:whatsthisappthing_i_have_no_idea_model_change", args=(4,))
```
