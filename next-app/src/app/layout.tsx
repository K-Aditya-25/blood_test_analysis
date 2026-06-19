import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "@/components/theme-provider";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Vitals — Your Blood Report, Visualized",
  description:
    "A calm, narrative visualization of your blood-test report with reference ranges, plain-language notes, and per-test charts.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme="light" suppressHydrationWarning>
      <body className={inter.variable}>
        <ThemeProvider
          attribute="data-theme"
          defaultTheme="light"
          enableSystem
          storageKey="bta-theme"
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
