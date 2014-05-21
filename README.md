DRFInlineExpansion
==================

Supporting Dynamic expansion of inline relationships when using the django rest framework


### Layout

`expand` module contains the code that does the work of adding inline expansion for nested relationships.
The rest of the code is the standard django rest framework tutorial code which uses the `expand` module as a demo.
`requirements.txt` lists the pip dependencies.

### Notes
* Take a look at `snippets/serializers.py` to see how `expandable_fields` attribute is used to specify the serializer that needs to be used when inline expansion is specified.
* Assuming you're running a test server with this code in port 8081, <http://localhost:8081/snippets/> will list the snippets populated in the SQLite database as a flat URL based representation.
* <http://localhost:8081/snippets/?expand=owner> will then expand the owner resource inline instead of using the URL representation
* <http://localhost:8081/snippets/?expand=owner,extra,extra.user> is another demo of inline expanion spanning multiple levels.
