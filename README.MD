# Fiosa Assistant

## What's the reason?
- Windows Copilot is coming out.
- Linux users don't have AI integration.
- Free software forever!

## The design
It is structured in 2 parts, the client and server. Why this approach? I chose it because we'll probably be using multiple different UIs for the assistant depending on the distro/DE. Therefore it makes sense to have a server rather than implementing the whole project from scratch in a different UI.

## Contribute??
If you'd like to contribute we are accepting input and changes in *any* of the source code. you can raise an issue or create a pull request. thanks :)
- if you're a prompt engineer feel free to take a look at System.MD (the system prompt)
- If you're a Python developer feel free to take a look at server.py (the heart of this project.)
- Also look at fiosa.py but it is obsolete.
### The project roadmap
(!) = priority
- [x] Running commands
- [x] Implement server and basic CLI client
- [ ] Create clients for desktop environments like GNOME (!)
- [ ] Look into using Microsoft Guidance framework to stop user perspective hallucinations
- [ ] create early builds of Linux distro
