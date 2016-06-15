import logging
import tornado.web
from mako.exceptions import RichTraceback

from eva.conf import settings


class RequestHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(RequestHandler, self).__init__(
            application, request, **kwargs)
        self.template_path = None
        self.title = None
        self.data = {}

    def render_string(self, template_path, **kwargs):
        namespace = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            # locale=self.locale,
            # _=self.locale.translate,
            # pgettext=self.locale.pgettext,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url,
            # custom
            s=lambda x: u"\"{0}\"".format(x),
        )

        # 如果标题未设置，设置一个默认值
        if self.title:
            namespace['title'] = self.title
        else:
            namespace['title'] = settings.DEFAULT_HTML_TITLE

        namespace.update(self.data)
        namespace.update(kwargs)

        try:
            html = self.application.template_lookup.get_template(
                template_path).render(**namespace)
        except:
            html = self.application.template_lookup.get_template(
                'mako_failed.html').render(
                    traceback=RichTraceback())

        return html

    def render(self, template_path=None, **kwargs):
        if not template_path:
            template_path = self.template_path
        html = self.render_string(template_path, **kwargs)
        self.finish(html)

    def get(self):
        '''提供默认的 HTTP GET 请求

        Python不太爱隐藏细节，但是程序员很懒。
        '''
        if self.template_path:
            self.render()
        else:
            # 可能 Handler 没有提供 get 方法
            logging.error('Can not find template_path in get method!')
            raise tornado.web.HTTPError(405)

    @property
    def api(self):
        return self.application.api
