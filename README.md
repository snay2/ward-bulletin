# Ward Bulletin Generator

These Python scripts generate a LaTeX document for a weekly LDS ward bulletin. The template uses legal size paper divided into six panels to create a tri-fold brochure.

## Usage

Invoke the generator like this:

    python generate.py bulletin.json

Make sure your `bulletin.json`, `lessons.json`, `primary.json`, `organizations.json`, and `calendar.json` files are up to date.

## Design

I chose only to use templating for the things that change from week to week. If you want to use this template for your own organization, you'll need to update the name and other static information in `template.tex`.

I wanted the config files to be such that I normally had to update almost every line, and the template such that I almost never had to modify it. This way it's easy to remember everything that needs to be updated and hard to mess up the things that shouldn't change.

