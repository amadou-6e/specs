# Visual Collaboration Workspace - Goal State

## Product goal

The long-term product is not a standalone text-erasure screen. It is a visual
collaboration workspace shared by the user and the AI agent through the SDK.
Both participants work against the same project files, page state, annotations,
editing layers, tools, and version history.

The workspace has three primary columns:

| Project and chat | Visual interaction space | Active editing tools |
| --- | --- | --- |
| Versioned file tree | Contextual page-editing tabs | Vertical tabs |
| Page selection | Image, layers, or Markdown editor | Annotate |
| User and agent chat | Direct manipulation and selection | Apply tools |

## Left column: project, versions, and conversation

- Show a filesystem view of the project and its versioned artifacts.
- Let the user select pages and Markdown documents from the file tree.
- Keep chat beside project history so requests remain grounded in the selected
  file and version.
- Make user changes and agent/SDK changes visible in the same version history.
- Selecting a page changes the center workspace to that page.
- Selecting a Markdown file opens it for writing in the center workspace.

The selected file is shared context. Chat actions, tool actions, annotations, and
agent review default to that file unless a different target is explicitly named.

### File System tab

The File System tab is a working project tree, not a read-only asset list.

- Show nested folders as a tree with independent expand and collapse controls.
- Allow selection of any file or folder.
- Allow users to create files and folders at the selected tree location.
- Allow users to rename, move, duplicate, edit, and delete project files.
- Provide a context menu and keyboard actions for common file operations.
- Keep the selected file visually highlighted and reveal its path in the center
  header and agent context.
- Refresh the tree after user actions and SDK or agent filesystem changes.
- Preserve expansion state while switching between files and versions.

File selection routes the center workspace by representation:

| Selected item | Center behavior |
| --- | --- |
| HTML page representation | Visual page canvas with Text, Layout, Color, Component, and Page Transition editing tabs |
| Markdown | Markdown source editor and optional rendered preview; no page-editing tabs |
| CSS, JavaScript, JSON, or other text | Source editor; no page-editing tabs |
| Raster or vector image | Image viewer and metadata unless opened through an HTML page representation |
| Unsupported binary | File metadata and download/open action |
| Folder | Folder summary, children, and create actions |

An HTML representation is the editable page surface. Selecting it must not open a
plain HTML viewer by default. It initializes or restores the page model, generated
editing layers, visual selections, and editing-mode tabs in the center workspace.
The user can still explicitly switch to HTML source when needed.

Recommended tree actions:

- New file
- New folder
- Rename
- Move or drag between folders
- Duplicate
- Open as visual page
- Open source
- Reveal related HTML representation
- Delete to recoverable trash

## Center column: contextual interaction space

For an image or design page:

- Show the visual page in the main stage.
- Show page-editing mode tabs above the stage.
- Automatically create the editing layers appropriate to that page.
- Let the user inspect, select, hide, lock, and edit those layers.
- Keep visual selections synchronized with chat and the right-side tools.

Automatically created layers can include:

- Source image
- Reconstructed background
- Detected text regions
- Editable or replacement text
- Masks and protected regions
- User annotations
- Agent suggestions or review overlays

For a Markdown document:

- Replace the visual stage with a Markdown writing and editing surface.
- Do not show image or page editing tabs above the center stage.
- Preserve the left project/chat column and relevant right-side tools.
- Treat Markdown as a first-class project page for notes, requirements,
  decisions, and agent collaboration.

| Selected item | Center content | Page editing tabs |
| --- | --- | --- |
| Image or design page | Visual canvas and generated layers | Visible |
| Markdown document | Markdown editor or preview | Hidden |
| Unsupported file | File preview and metadata | Hidden |
| No selection | Project onboarding or empty state | Hidden |

## Right column: tools for the active editing mode

- Present one tool per vertical tab for the currently selected center editing mode.
- Changing the center editing mode changes the tools available in the right pane.
- The current design focus is Text Editing, whose initial tools are OCR, TMIM,
  Font Matcher, and Export.
- Let the user annotate the current page for AI-agent review.
- Let the user directly run the same tools available to the agent.
- Attach tool input and output to the selected file, page, layer, and version.
- Clearly distinguish a proposed annotation, a preview, and an applied change.

A tool must not have separate user and agent implementations. The interface and
SDK invoke the same underlying operation with the same parameters and produce the
same versioned artifact. This implementation sharing does not define the pane's
information architecture: the pane is organized by active editing mode and tool.

Editing modes may provide tools such as:

1. Review and annotate - point, rectangle, freehand, comment, approve, reject.
2. Text - detect, erase, export to HTML, modify, and manual background fill.
3. Layout - inspect structure, move or resize regions, and manage page layers.
4. Masks and regions - add, subtract, protect, merge, or refine selections.
5. History and output - preview, compare versions, apply, revert, and export.

## Collaboration contract

Every meaningful operation provides enough structured context for either the user
or agent to continue:

- Active project and selected file
- Active page and version
- Active editing mode and visible layers
- Current selection or annotated region
- Tool name and parameters
- Preview or output artifact
- Apply, reject, undo, and redo state
- Chat message or rationale associated with the operation

Annotations must be addressable from chat. A user can mark a region and say
remove this residual, while the agent receives the exact page, version,
coordinates, and annotation identifier through the SDK.

Agent proposals appear as inspectable page annotations or preview layers that the
user can approve, modify, or reject.

## Required behavior

- File selection is the primary navigation mechanism.
- File tree and chat persist while moving between pages.
- The left and right panes can collapse horizontally to maximize the canvas.
- Sections within a pane can collapse vertically while retaining their headers.
- Pane and section collapse affordances are sleek structural bars, not standalone
  buttons: vertical bars collapse side panes horizontally and horizontal bars
  collapse stacked fields vertically.
- File System, Git History, and Chat are stacked sections in the left pane, not a
  mutually exclusive tab switcher.
- Page layers are created automatically and stored as page state.
- Editing tabs derive from the selected file type and available layers.
- Selecting Markdown suppresses all image-editing tabs.
- Right-pane tools are scoped to the active center editing mode.
- User and agent invocations share one operation API.
- All applied operations create recoverable versions.
- Annotations are persistent, version-aware, and available to the SDK.
- The interface clearly distinguishes previews from committed changes.
- The active selection is visible to both the browser interface and agent context.

## Relationship to the current Text Tool

The existing erase-text experience becomes one page-editing mode and one shared
tool group inside this larger workspace. Its OCR stages, masks, reconstructed
background, final result, and manual cleanup regions should become inspectable
layers and versioned operations instead of isolated pipeline images.

The editable workspace proposal is maintained in 	ext-tool-layouts.drawio.
The current text-tool-specific states remain documented in LAYOUT.md.
