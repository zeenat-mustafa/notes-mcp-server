# Personal Notes Manager — MCP Server

A simple MCP (Model Context Protocol) server that lets an AI assistant create, list, retrieve, search, and delete personal notes.

## What it does

This server exposes 5 tools and 1 read-only resource for managing a small notes collection. Notes are stored in a plain JSON file (`notes_data.json`) — no database required.

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/zeenat-mustafa/notes-mcp-server.git
   cd notes-mcp-server
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\Activate.ps1      # Windows PowerShell
   source venv/bin/activate       # Mac/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the server:
   ```
   python server.py
   ```
   The server communicates over stdio and is meant to be connected to by an MCP client (like MCP Inspector or an AI assistant), not run standalone.

## Testing with MCP Inspector

```
npx @modelcontextprotocol/inspector python server.py
```
Then open the URL it prints, connect, and try the tools below.

## Tools

### `create_note(title, body)`
Creates a new note.
Example: `create_note(title="Grocery list", body="Milk, eggs, bread")`
→ `Created note #1: "Grocery list"`

### `list_notes()`
Lists all notes by id and title. Takes no input.
Example: `list_notes()`
→ `#1: Grocery list`

### `get_note(note_id)`
Retrieves the full title and body of one note.
Example: `get_note(note_id=1)`
→ `#1: Grocery list\n\nMilk, eggs, bread`

### `search_notes(query)`
Searches note titles and bodies for a keyword (case-insensitive).
Example: `search_notes(query="grocery")`
→ `#1: Grocery list`

### `delete_note(note_id)`
Deletes a note by id.
Example: `delete_note(note_id=1)`
→ `Deleted note #1: "Grocery list"`

## Resource

### `notes://all`
A read-only view of every note currently stored, including full bodies.

## Error handling

Every tool checks its input and returns a clear error message instead of crashing:
- Empty title/body on `create_note` → `"Error: title cannot be empty."`
- Empty search query on `search_notes` → `"Error: search query cannot be empty."`
- Unknown `note_id` on `get_note` / `delete_note` → `"Error: no note found with id X."`

## Storage

Notes are stored in `notes_data.json`, created automatically the first time a note is saved. Each note has an `id`, `title`, and `body`.

## Tech stack

- Python 3.10+
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (`mcp<2`, using the `FastMCP` API)