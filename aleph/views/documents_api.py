from werkzeug.exceptions import BadRequest
from flask import Blueprint, redirect, send_file, request
from apikit import jsonify, Pager, get_limit, get_offset

from aleph.core import get_archive
from aleph import authz
from aleph.model import Document
from aleph.views.cache import enable_cache
from aleph.search.tabular import tabular_query, execute_tabular_query
from aleph.views.util import get_document, match_ids
from aleph.views.util import get_tabular, get_page


blueprint = Blueprint('documents_api', __name__)


@blueprint.route('/api/1/documents', methods=['GET'])
def index():
    sources_ids = match_ids('sources', authz.sources(authz.READ))
    q = Document.all().filter(Document.source_id.in_(sources_ids))
    hashes = request.args.getlist('content_hash')
    if len(hashes):
        q = q.filter(Document.content_hash.in_(hashes))
    return jsonify(Pager(q))


@blueprint.route('/api/1/documents/<int:document_id>')
def view(document_id):
    doc = get_document(document_id)
    enable_cache()
    data = doc.to_dict()
    data['source'] = doc.source
    return jsonify(data)


@blueprint.route('/api/1/documents/<int:document_id>/file')
def file(document_id):
    document = get_document(document_id)
    enable_cache(server_side=True)
    url = get_archive().generate_url(document.meta)
    if url is not None:
        return redirect(url)

    local_path = get_archive().load_file(document.meta)
    fh = open(local_path, 'rb')
    return send_file(fh, as_attachment=True,
                     attachment_filename=document.meta.file_name,
                     mimetype=document.meta.mime_type)


@blueprint.route('/api/1/documents/<int:document_id>/pdf')
def pdf(document_id):
    document = get_document(document_id)
    enable_cache(server_side=True)
    if document.type != Document.TYPE_TEXT:
        raise BadRequest("PDF is only available for text documents")
    pdf = document.meta.pdf
    url = get_archive().generate_url(pdf)
    if url is not None:
        return redirect(url)

    local_path = get_archive().load_file(pdf)
    fh = open(local_path, 'rb')
    return send_file(fh, mimetype=pdf.mime_type)


@blueprint.route('/api/1/documents/<int:document_id>/pages/<int:number>')
def page(document_id, number):
    document, page = get_page(document_id, number)
    enable_cache(server_side=True)
    return jsonify(page)


@blueprint.route('/api/1/documents/<int:document_id>/tables/<int:table_id>')
def table(document_id, table_id):
    document, tabular = get_tabular(document_id, table_id)
    enable_cache(vary_user=True)
    return jsonify(tabular)


@blueprint.route('/api/1/documents/<int:document_id>/tables/<int:table_id>/rows')
def rows(document_id, table_id):
    document, tabular = get_tabular(document_id, table_id)
    query = tabular_query(document_id, table_id, request.args)
    query['size'] = get_limit(default=100)
    query['from'] = get_offset()
    return jsonify(execute_tabular_query(document_id, table_id,
                                         request.args, query))