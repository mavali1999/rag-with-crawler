from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


class Chunker:

    def split_markdown(self, markdown_document):

        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
        ]

        # MD splits
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, 
            strip_headers=False,
            # return_each_line=True,
        )
        md_header_splits = markdown_splitter.split_text(markdown_document)

        # Char-level splits
        chunk_size = 1000
        chunk_overlap = 200
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap,
        )

        # Split
        splits = text_splitter.split_documents(md_header_splits)
        
        return splits
    
    def remove_small_chunks(self, documents):

        length_threshold = 100
        
        new_documents = []
        for doc in documents:
            if len(doc.page_content) >= length_threshold:
                new_documents.append(doc)
        
        return new_documents
