from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound


# pylint: disable=too-few-public-methods
class MailPaginator:
    #pylint: disable=R0201
    def paginate_objects(self, instance, page_no):
        paginator = Paginator(instance, 10)

        try:
            mail_per_page = paginator.get_page(page_no)

        except PageNotAnInteger:
            mail_per_page = paginator.get_page(1)

        except EmptyPage:
            mail_per_page = paginator.get_page(Paginator.num_pages)

        if mail_per_page.has_next():
            next_page_number = mail_per_page.next_page_number()
        else:
            next_page_number = None

        if mail_per_page.has_previous():
            previous_page_number = mail_per_page.previous_page_number()
        else:
            previous_page_number = None

        mails = {
            "results": mail_per_page.object_list,
            "has_next": mail_per_page.has_next(),
            "has_previous": mail_per_page.has_previous(),
            "next_page_number": next_page_number,
            "previous_page_number": previous_page_number,
            "start_index": mail_per_page.start_index(),
            "end_index": mail_per_page.end_index(),
            "num_page": paginator.num_pages,
            "count": paginator.count,
            "count_per_page": paginator.count * paginator.num_pages,
        }

        return mails


class SmallPagesPagination(PageNumberPagination):
    page_size = 5

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        # page_size = self.get_page_size(request)
        page_size = request.GET.get("page_size")
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data, *args, **kwargs):
        if args is not None:
            return Response({
                'results': data,
                'count-stats' : args,
                "has_next": self.page.has_next(),
                "has_previous": self.page.has_previous(),
                "next_page_number": self.get_next_link(),
                "previous_page_number": self.get_previous_link(),
                "start_index": self.page.start_index(),
                "end_index": self.page.end_index(),
                "num_page": self.page.paginator.num_pages,
                'count': self.page.paginator.count,
                "count_per_page": self.page.paginator.count * self.page.paginator.num_pages,
                # 'limit': self.get_page_size()
            })
        else:
            return Response({
                'results': data,
                "has_next": self.page.has_next(),
                "has_previous": self.page.has_previous(),
                "next_page_number": self.get_next_link(),
                "previous_page_number": self.get_previous_link(),
                "start_index": self.page.start_index(),
                "end_index": self.page.end_index(),
                "num_page": self.page.paginator.num_pages,
                'count': self.page.paginator.count,
                "count_per_page": self.page.paginator.count * self.page.paginator.num_pages,
                #'limit': self.get_page_size()
            })

    def get_next_link(self):
        if not self.page.has_next():
            return None

        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()

        return page_number
