# Package: triorb_stub_pico

triorb_drive_picoの代替ノード

値をpublishするときその都度/triorb/params/stub_pico_io.jsonを参照して値を返す <br>
例外的にnullを入れると他のパラメータを考慮して値を返す <br>
例えば、/robot/statusの励磁状態に対応するbitフラグは TriOrbBaseStateのB0キーを参照する。 <br>
このキーを"B0": null とすると、/drive/wakeupや/drive/sleepのトピックsubscribeに応じて変更されるようになる。 <br>
