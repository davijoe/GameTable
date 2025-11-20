import { Card, CardBody, Heading, Image } from "@chakra-ui/react";
import type { Game } from "../../entities/Game";

interface Props {
  game: Game;
}

export const GameCard = ({ game }: Props) => {
    return (
        <Card>
            <Image src={" https://cf.geekdo-images.com/x3zxjr-Vw5iU4yDPg70Jgw__small/img/o18rjEemoWaVru9Y2TyPwuIaRfE=/fit-in/200x150/filters:strip_icc()/pic3490053.jpg"}></Image>
            <CardBody>
                <Heading fontSize={"2x1"}>
                    Test Name
                </Heading>
            </CardBody>
        </Card>)

}