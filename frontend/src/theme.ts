import { extendTheme, type ThemeConfig } from "@chakra-ui/react";

const config: ThemeConfig = {
  initialColorMode: "dark",
};

const colors = {
  brand: {
    50: "#f5f3ff3f",
    100: "#ede9fe",
    200: "#d6c2fc",
    300: "#b08bf9",
    400: "#8b54f6",
    500: "#7c3aed",
    600: "#6d28d9",
    700: "#5b21b6",
  },
};

//used for the Chakra styling
const components = {
  Tabs: {
    variants: {
      "solid-rounded": {
        tab: {
          color: "white",
          _selected: {
            bg: "brand.500",
            color: "white",
          },
          _hover: {
            bg: "brand.50",
            _selected: {
              bg: "brand.500",
            },
          },
        },
      },
    },
  },
};

//used for the background
const styles = {
  global: {
    "html, body, #root": {
      height: "100%",
      margin: 0,
    },
    body: {
      bg: "linear-gradient(135deg, #161933 0%, #5A178B 50%, #161933 100%)",
      bgSize: "cover",
      bgAttachment: "fixed",
      color: "white",
    },
  },
};

const theme = extendTheme({ config, colors, styles, components });

export default theme;
