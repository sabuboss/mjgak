import type { Metadata } from "next";

import { MyClient } from "./MyClient";

export const metadata: Metadata = { title: "내 정보", robots: { index: false } };

export default function MyPage() {
  return <MyClient />;
}
