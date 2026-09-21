# Hinweise für Claude in diesem Repo

## Dateinamen von Regelkarten nie kürzen

Wenn Regelkarten-PPTX (oder deren Markdown-/JSON-Zwillinge) im Chat, als ZIP
oder auf andere Weise herausgegeben werden, immer den vollständigen
Dateinamen nach dem Schema des Generators verwenden:

```
RK-0xx_kurztitel_r0x.pptx
```

Beispiel: `RK-012_wer-darf-eine-maschine-starten_r01.pptx` — **nicht**
`RK-012.pptx`. Der Kurztitel steht schon in der Datei drin (oder in ihrem
Dateinamen, falls sie schon einmal existiert hat) und darf beim Kopieren,
Umbenennen oder Weiterreichen nicht verloren gehen, auch nicht für
Zwischenschritte in einem Scratchpad.
