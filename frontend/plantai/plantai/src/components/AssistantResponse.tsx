interface AssistantResponseProps {
  text: string;
}

function renderInline(text: string) {
  return text.split(/(\*\*[^*]+\*\*)/g).map((part, index) =>
    part.startsWith('**') && part.endsWith('**') ? (
      <strong key={index} className="font-bold text-[#234a2d]">{part.slice(2, -2)}</strong>
    ) : part,
  );
}

export default function AssistantResponse({text}: AssistantResponseProps) {
  const blocks = text.trim().split(/\n\s*\n/).filter(Boolean);

  return <div className="space-y-3 text-[15px] leading-7 text-[#415247]">
    {blocks.map((block, index) => {
      const lines = block.split('\n').map(line => line.trim()).filter(Boolean);
      const heading = lines.length === 1 && /^#{1,3}\s/.test(lines[0]);
      const list = lines.every(line => /^[-*]\s|^\d+[.)]\s/.test(line));

      if (heading) return <h3 key={index} className="font-display text-base font-extrabold text-[#234a2d]">{renderInline(lines[0].replace(/^#{1,3}\s/, ''))}</h3>;

      if (list) {
        const ordered = /^\d+[.)]\s/.test(lines[0]);
        const ListTag = ordered ? 'ol' : 'ul';
        return <ListTag key={index} className={`${ordered ? 'list-decimal' : 'list-disc'} space-y-1.5 pl-5 marker:text-[#6fae68]`}>
          {lines.map((line, lineIndex) => <li key={lineIndex}>{renderInline(line.replace(/^(?:[-*]|\d+[.)])\s/, ''))}</li>)}
        </ListTag>;
      }

      return <p key={index}>{lines.map((line, lineIndex) => <span key={lineIndex}>{lineIndex > 0 && <br />}{renderInline(line)}</span>)}</p>;
    })}
  </div>;
}