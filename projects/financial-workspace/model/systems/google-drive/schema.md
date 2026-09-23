# Google-Drive schema

## Identity and fields

A usable observation requires the Drive workspace scope, native file ID, namespaced `drive:<file_id>` source ID, observation time, and availability. Optional observed fields include URL, name, MIME type, size, modified time, parent ID, path, owner/account context, document date, coverage, provider hashes, and SHA-256.

The native file ID is the stable key. IDs are opaque and retained exactly. URLs are locators; paths, names, parents, sizes, modified times, and hashes are observations. Matching metadata may support a reviewed alias but cannot merge two IDs automatically. Equal hashes establish byte equality, not logical identity.

