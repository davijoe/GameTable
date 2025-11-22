import type { ReactNode } from "react";
import { AspectRatio, Card, CardBody } from "@chakra-ui/react";

type GameCardBaseProps = {
  image?: ReactNode;
  children?: ReactNode;
};

export const GameCardBase = ({ image, children }: GameCardBaseProps) => {
  return (
    <Card>
      <AspectRatio ratio={4 / 4} width="100%">
        {image}
      </AspectRatio>
      <CardBody>{children}</CardBody>
    </Card>
  );
};