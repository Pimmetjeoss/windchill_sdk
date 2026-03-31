const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber } = require('docx');
const fs = require('fs');

const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 48, bold: true, color: "1F3864", font: "Arial" },
        paragraph: { spacing: { before: 0, after: 200 }, alignment: AlignmentType.LEFT } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: "1F3864", font: "Arial" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, color: "2E5090", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [
      { reference: "steps",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "steps2",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "bullets2",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    properties: {
      page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "Windchill MCP Server - Installatiehandleiding", italics: true, size: 18, color: "888888" })]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Pagina ", size: 18 }), new TextRun({ children: [PageNumber.CURRENT], size: 18 }), new TextRun({ text: " van ", size: 18 }), new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18 })]
      })] })
    },
    children: [
      // Title
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Windchill MCP Server")] }),
      new Paragraph({ spacing: { after: 400 }, children: [
        new TextRun({ text: "Installatiehandleiding voor Claude Desktop", size: 28, color: "666666" })
      ]}),

      // Wat is dit?
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Wat is dit?")] }),
      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun("De Windchill MCP Server is een uitbreiding voor Claude Desktop waarmee je in gewoon Nederlands vragen kunt stellen over data in Windchill PLM. Denk aan:")
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Parts en documenten opzoeken")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Openstaande Change Requests en Change Tasks bekijken")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Workflow taken (Validate for SAP) inzien")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("Impact analyses van change tasks uitvoeren")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun("PDF documenten downloaden vanuit Windchill")] }),
      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun({ text: "Je hoeft geen OData queries of API-kennis te hebben. Je vraagt het gewoon aan Claude.", italics: true })
      ]}),

      // Vereisten
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Vereisten")] }),
      new Paragraph({ numbering: { reference: "bullets2", level: 0 }, children: [
        new TextRun({ text: "Claude Desktop", bold: true }), new TextRun(" geinstalleerd (download via claude.ai/download)")
      ]}),
      new Paragraph({ numbering: { reference: "bullets2", level: 0 }, children: [
        new TextRun({ text: "Python 3.11+", bold: true }), new TextRun(" geinstalleerd (download via python.org)")
      ]}),
      new Paragraph({ numbering: { reference: "bullets2", level: 0 }, children: [
        new TextRun({ text: "VPN-verbinding", bold: true }), new TextRun(" met het Contiweb netwerk (voor toegang tot plm.contiweb.com)")
      ]}),
      new Paragraph({ numbering: { reference: "bullets2", level: 0 }, spacing: { after: 200 }, children: [
        new TextRun({ text: "Windchill account", bold: true }), new TextRun(" (je gebruikelijke gebruikersnaam en wachtwoord)")
      ]}),

      // Installatie - Automatisch
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Installatie (automatisch)")] }),
      new Paragraph({ numbering: { reference: "steps", level: 0 }, children: [
        new TextRun("Pak het ZIP-bestand uit naar een map, bijvoorbeeld "),
        new TextRun({ text: "C:\\windchill_sdk", bold: true })
      ]}),
      new Paragraph({ numbering: { reference: "steps", level: 0 }, children: [
        new TextRun("Open een terminal (Command Prompt of PowerShell) in die map")
      ]}),
      new Paragraph({ numbering: { reference: "steps", level: 0 }, children: [
        new TextRun("Voer het volgende commando uit:"),
      ]}),
      new Paragraph({ spacing: { before: 100, after: 100 }, indent: { left: 1080 }, children: [
        new TextRun({ text: "python scripts\\install.py", font: "Consolas", size: 22, bold: true, color: "1F3864",
          shading: { type: ShadingType.CLEAR, fill: "F0F0F0" } })
      ]}),
      new Paragraph({ numbering: { reference: "steps", level: 0 }, children: [
        new TextRun("Het script vraagt om je "),
        new TextRun({ text: "Windchill gebruikersnaam", bold: true }),
        new TextRun(" en "),
        new TextRun({ text: "wachtwoord", bold: true }),
        new TextRun(". Deze worden alleen lokaal opgeslagen.")
      ]}),
      new Paragraph({ numbering: { reference: "steps", level: 0 }, children: [
        new TextRun({ text: "Herstart Claude Desktop", bold: true }),
        new TextRun(" (volledig afsluiten en opnieuw openen)")
      ]}),
      new Paragraph({ numbering: { reference: "steps", level: 0 }, spacing: { after: 200 }, children: [
        new TextRun("Test door Claude te vragen: "),
        new TextRun({ text: "\"Welke containers zijn er in Windchill?\"", italics: true, color: "1F3864" })
      ]}),

      // Installatie - Handmatig
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Installatie (handmatig)")] }),
      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun("Als het automatische script niet werkt, kun je de configuratie handmatig doen.")
      ]}),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Stap 1: SDK installeren")] }),
      new Paragraph({ spacing: { after: 100 }, children: [new TextRun("Open een terminal in de map waar je het ZIP-bestand hebt uitgepakt en voer uit:")] }),
      new Paragraph({ spacing: { after: 200 }, indent: { left: 720 }, children: [
        new TextRun({ text: "pip install -e .[mcp]", font: "Consolas", size: 22, bold: true, color: "1F3864",
          shading: { type: ShadingType.CLEAR, fill: "F0F0F0" } })
      ]}),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Stap 2: Claude Desktop configureren")] }),
      new Paragraph({ spacing: { after: 100 }, children: [new TextRun("Open het configuratiebestand van Claude Desktop:")] }),
      new Paragraph({ spacing: { after: 200 }, indent: { left: 720 }, children: [
        new TextRun({ text: "%APPDATA%\\Claude\\claude_desktop_config.json", font: "Consolas", size: 20,
          shading: { type: ShadingType.CLEAR, fill: "F0F0F0" } })
      ]}),
      new Paragraph({ spacing: { after: 100 }, children: [new TextRun("Voeg het volgende blok toe (of maak het bestand aan):")] }),

      // JSON config block
      new Paragraph({ indent: { left: 720 }, children: [new TextRun({ text: "{", font: "Consolas", size: 20 })] }),
      new Paragraph({ indent: { left: 1080 }, children: [new TextRun({ text: "\"mcpServers\": {", font: "Consolas", size: 20 })] }),
      new Paragraph({ indent: { left: 1440 }, children: [new TextRun({ text: "\"windchill\": {", font: "Consolas", size: 20 })] }),
      new Paragraph({ indent: { left: 1800 }, children: [new TextRun({ text: "\"command\": \"python\",", font: "Consolas", size: 20 })] }),
      new Paragraph({ indent: { left: 1800 }, children: [new TextRun({ text: "\"args\": [\"C:\\\\pad\\\\naar\\\\windchill_sdk\\\\run_mcp.py\"],", font: "Consolas", size: 20 })] }),
      new Paragraph({ indent: { left: 1800 }, children: [new TextRun({ text: "\"env\": {", font: "Consolas", size: 20 })] }),
      new Paragraph({ indent: { left: 2160 }, children: [new TextRun({ text: "\"WINDCHILL_BASE_URL\": \"https://plm.contiweb.com/Windchill/servlet/odata\",", font: "Consolas", size: 18 })] }),
      new Paragraph({ indent: { left: 2160 }, children: [new TextRun({ text: "\"WINDCHILL_USERNAME\": \"jouw_gebruikersnaam\",", font: "Consolas", size: 18 })] }),
      new Paragraph({ indent: { left: 2160 }, children: [new TextRun({ text: "\"WINDCHILL_PASSWORD\": \"jouw_wachtwoord\",", font: "Consolas", size: 18 })] }),
      new Paragraph({ indent: { left: 2160 }, children: [new TextRun({ text: "\"WINDCHILL_VERIFY_SSL\": \"false\",", font: "Consolas", size: 18 })] }),
      new Paragraph({ indent: { left: 2160 }, children: [new TextRun({ text: "\"WINDCHILL_API_VERSION\": \"3\"", font: "Consolas", size: 18 })] }),
      new Paragraph({ indent: { left: 1800 }, children: [new TextRun({ text: "}", font: "Consolas", size: 20 })] }),
      new Paragraph({ indent: { left: 1440 }, children: [new TextRun({ text: "}", font: "Consolas", size: 20 })] }),
      new Paragraph({ indent: { left: 1080 }, children: [new TextRun({ text: "}", font: "Consolas", size: 20 })] }),
      new Paragraph({ indent: { left: 720 }, spacing: { after: 200 }, children: [new TextRun({ text: "}", font: "Consolas", size: 20 })] }),

      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun({ text: "Let op: ", bold: true }),
        new TextRun("Vervang het pad en je credentials. Gebruik dubbele backslashes (\\\\) in Windows paden.")
      ]}),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Stap 3: Herstart Claude Desktop")] }),
      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun("Sluit Claude Desktop volledig af en open het opnieuw. De Windchill tools zijn nu beschikbaar.")
      ]}),

      // Wat kun je vragen?
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Wat kun je vragen aan Claude?")] }),

      new Table({
        columnWidths: [4680, 4680],
        rows: [
          new TableRow({ tableHeader: true, children: [
            new TableCell({ borders: cellBorders, width: { size: 4680, type: WidthType.DXA },
              shading: { fill: "1F3864", type: ShadingType.CLEAR },
              children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Wat je wilt", bold: true, color: "FFFFFF", size: 22 })] })] }),
            new TableCell({ borders: cellBorders, width: { size: 4680, type: WidthType.DXA },
              shading: { fill: "1F3864", type: ShadingType.CLEAR },
              children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Voorbeeldvraag", bold: true, color: "FFFFFF", size: 22 })] })] }),
          ]}),
          ...[
            ["Part opzoeken", "\"Zoek part WH806239\""],
            ["Document downloaden", "\"Download de PDF van WH806239\""],
            ["Open change requests", "\"Welke change requests staan open?\""],
            ["Change task details", "\"Geef me details van CT015630\""],
            ["Impact analyse", "\"Doe een impact analyse van CT015630\""],
            ["Open workflow taken", "\"Welke Validate for SAP taken staan open?\""],
            ["Containers bekijken", "\"Welke containers zijn er in Windchill?\""],
            ["Documenten zoeken", "\"Zoek documenten met FD-1460 in de naam\""],
            ["Gebruikers zoeken", "\"Zoek gebruiker Rudy\""],
          ].map(([wat, vraag]) => new TableRow({ children: [
            new TableCell({ borders: cellBorders, width: { size: 4680, type: WidthType.DXA },
              children: [new Paragraph({ children: [new TextRun({ text: wat, size: 22 })] })] }),
            new TableCell({ borders: cellBorders, width: { size: 4680, type: WidthType.DXA },
              children: [new Paragraph({ children: [new TextRun({ text: vraag, italics: true, color: "1F3864", size: 22 })] })] }),
          ]}))
        ]
      }),

      // Veiligheid
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Veiligheid")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun("De MCP server draait "),
        new TextRun({ text: "lokaal op je eigen PC", bold: true }),
        new TextRun(" als een Python process")
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun("Alle Windchill API calls gaan "),
        new TextRun({ text: "direct van jouw PC naar plm.contiweb.com", bold: true }),
        new TextRun(" via de VPN")
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [
        new TextRun("Je credentials worden "),
        new TextRun({ text: "alleen lokaal opgeslagen", bold: true }),
        new TextRun(" en verlaten je PC nooit")
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [
        new TextRun("Tool-resultaten (part data, change requests) worden naar Anthropic gestuurd zodat Claude een antwoord kan formuleren")
      ]}),

      // Verwijderen
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Verwijderen")] }),
      new Paragraph({ spacing: { after: 100 }, children: [new TextRun("Om de Windchill MCP server te verwijderen, voer uit:")] }),
      new Paragraph({ spacing: { after: 200 }, indent: { left: 720 }, children: [
        new TextRun({ text: "python scripts\\uninstall.py", font: "Consolas", size: 22, bold: true, color: "1F3864",
          shading: { type: ShadingType.CLEAR, fill: "F0F0F0" } })
      ]}),
      new Paragraph({ spacing: { after: 200 }, children: [new TextRun("Of verwijder handmatig het \"windchill\" blok uit claude_desktop_config.json.")] }),

      // Problemen
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Problemen?")] }),

      new Table({
        columnWidths: [3120, 6240],
        rows: [
          new TableRow({ tableHeader: true, children: [
            new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA },
              shading: { fill: "1F3864", type: ShadingType.CLEAR },
              children: [new Paragraph({ children: [new TextRun({ text: "Probleem", bold: true, color: "FFFFFF", size: 22 })] })] }),
            new TableCell({ borders: cellBorders, width: { size: 6240, type: WidthType.DXA },
              shading: { fill: "1F3864", type: ShadingType.CLEAR },
              children: [new Paragraph({ children: [new TextRun({ text: "Oplossing", bold: true, color: "FFFFFF", size: 22 })] })] }),
          ]}),
          ...[
            ["Claude ziet geen Windchill tools", "Herstart Claude Desktop volledig (afsluiten + opnieuw openen)"],
            ["SSL/certificaat fout", "Controleer of WINDCHILL_VERIFY_SSL op \"false\" staat in de config"],
            ["Authenticatie mislukt", "Controleer gebruikersnaam en wachtwoord in de config"],
            ["Geen verbinding met Windchill", "Controleer of je VPN-verbinding actief is"],
            ["Python niet gevonden", "Installeer Python 3.11+ via python.org en herstart de terminal"],
          ].map(([probleem, oplossing]) => new TableRow({ children: [
            new TableCell({ borders: cellBorders, width: { size: 3120, type: WidthType.DXA },
              children: [new Paragraph({ children: [new TextRun({ text: probleem, size: 22 })] })] }),
            new TableCell({ borders: cellBorders, width: { size: 6240, type: WidthType.DXA },
              children: [new Paragraph({ children: [new TextRun({ text: oplossing, size: 22 })] })] }),
          ]}))
        ]
      }),

      new Paragraph({ spacing: { before: 400 }, children: [
        new TextRun({ text: "Vragen? Neem contact op met Pim Lieshout.", italics: true, color: "888888" })
      ]}),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("Windchill MCP Server - Installatiehandleiding.docx", buffer);
  console.log("Document created: Windchill MCP Server - Installatiehandleiding.docx");
});
