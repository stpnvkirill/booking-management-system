interface MessageProps {
  message: string | undefined;
}

export default function Message({ message }: MessageProps) {
  return <div className="text-center">{message}</div>;
}
