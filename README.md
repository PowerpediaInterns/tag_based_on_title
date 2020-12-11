# tag_based_on_title
Tags a desired Namespace with a category based on its title

## Class variables for customization
### NAMESPACE
The namespace that the program will extract pages from (e.g. 0 for (Main)).\
https://www.mediawiki.org/wiki/Manual:Namespace#Built-in_namespaces to see available namespaces.

### PAGES_LIMIT
The number of pages that will be extracted at a time. Used in get_pages_json() in params for "aplimit".
