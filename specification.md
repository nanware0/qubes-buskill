# Specification policy

## What's the specification and why apply it?

First thing to say: **it's not formal specification** - we don't use that.  
This specification consist in **commenting every step of the code** and what **it should do**, so if we want to audit it, we can verify that **the code and the specification matches.** Then, we can verify if the specification is correct, and if it is, the code *should* be good.  
The other good point is that everyone will be able to understand what the code do, but there is also a bad point: it's rarely fun to write this specification, I know.

## How to write a specification?

If you want to comment a line, add comments at the end of the line or just before the line. **DO NOT** add comments **after the line:** it must be before or at the end, **NEVER after.**

Also, it is important to document your functions and classes, even if this is not in the scope of the specification, it is useful to know what's their purpose and what they do.