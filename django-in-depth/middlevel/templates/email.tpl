{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ name }}<h1>H1!</h1>
{% endblock %}

{% block body %}
{{ name }}, this is a plain text message.
<h1>H1!</h1>
{% endblock %}

{% block html %}
{{ name }}, this is an <strong>html</strong> message.
<h1>H1!</h1>
{% endblock %}
