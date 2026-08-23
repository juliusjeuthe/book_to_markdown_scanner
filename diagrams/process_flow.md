# Process Flow: Book to Markdown Scanner

```mermaid
flowchart TD
  subgraph Scanning [Part 1 — Scanning]
    A[vFlat Scan<br/>Export images] --> B[images_that_should_be_impored]
  end

  subgraph Conversion [Part 2 — OCR & Conversion]
    B --> C[Preprocess image<br/>(deskew, denoise, binarize)]
    C --> D[OCR engine<br/>(pytesseract / easyocr)]
    D --> H{OCR success?}
    H -- yes --> E[Create Markdown file<br/>Insert tag: #{to_be_proof_read}]
    E --> F[exported_markdown_files]
    E --> G[Update image_to_markdown_page_map.md<br/>(image → md → page → converted_at)]
    H -- no --> I[Save debug image in failed/]
    I --> G
  end

  subgraph Proofreading [Part 3 — Copilot Proofreading]
    F --> J[Copilot / Manual Review]
    J --> K{Approved?}
    K -- yes --> L[Replace tag with #{validated_by_copilot}]
    K -- no --> M[Edit markdown or re-run conversion]
    L --> G[Update map: validated_at, validated_by]
    M --> D
  end

  style Scanning fill:#f9f,stroke:#333,stroke-width:1px
  style Conversion fill:#fffae6,stroke:#333,stroke-width:1px
  style Proofreading fill:#e6fff2,stroke:#333,stroke-width:1px
```
