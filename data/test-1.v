/* Generated by Yosys 0.41 (git sha1 c1ad37779ee, clang++ 15.0.0 -fPIC -Os) */

module top_809960632_810038711_1598227639_893650103(n2, n4, n6, n9, n12, n18, n22, n34, n35, n42, n48, n51, n56, n57, n65, n67, n68, n72, n75, n77, n78
, n80);
  wire _000_;
  wire _001_;
  wire _002_;
  wire _003_;
  wire _004_;
  wire _005_;
  wire _006_;
  wire _007_;
  wire _008_;
  wire _009_;
  wire _010_;
  wire _011_;
  wire _012_;
  wire _013_;
  wire _014_;
  wire _015_;
  wire _016_;
  wire _017_;
  wire _018_;
  wire _019_;
  wire _020_;
  wire _021_;
  wire _022_;
  wire _023_;
  wire _024_;
  wire _025_;
  wire _026_;
  wire _027_;
  wire _028_;
  wire _029_;
  wire _030_;
  wire _031_;
  wire _032_;
  wire _033_;
  wire _034_;
  wire _035_;
  wire _036_;
  wire _037_;
  wire _038_;
  wire _039_;
  wire _040_;
  wire _041_;
  wire _042_;
  wire _043_;
  wire _044_;
  wire _045_;
  wire _046_;
  wire _047_;
  wire _048_;
  wire _049_;
  wire _050_;
  wire _051_;
  wire _052_;
  wire _053_;
  wire _054_;
  wire _055_;
  wire _056_;
  wire _057_;
  wire _058_;
  wire _059_;
  wire _060_;
  wire _061_;
  wire _062_;
  wire _063_;
  wire _064_;
  wire _065_;
  wire _066_;
  wire _067_;
  wire _068_;
  wire _069_;
  wire _070_;
  wire _071_;
  input n12;
  wire n12;
  input n18;
  wire n18;
  input n2;
  wire n2;
  input n22;
  wire n22;
  input n34;
  wire n34;
  input n35;
  wire n35;
  input n4;
  wire n4;
  output n42;
  wire n42;
  output n48;
  wire n48;
  input n51;
  wire n51;
  output n56;
  wire n56;
  input n57;
  wire n57;
  output n6;
  wire n6;
  output n65;
  wire n65;
  input n67;
  wire n67;
  output n68;
  wire n68;
  input n72;
  wire n72;
  input n75;
  wire n75;
  output n77;
  wire n77;
  input n78;
  wire n78;
  input n80;
  wire n80;
  output n9;
  wire n9;
  not_1 _072_ (
    n4,
    _002_
  );
  not_1 _073_ (
    n51,
    _003_
  );
  not_1 _074_ (
    n57,
    _004_
  );
  not_1 _075_ (
    n2,
    _005_
  );
  not_1 _076_ (
    n67,
    _006_
  );
  not_1 _077_ (
    n72,
    _007_
  );
  nand_1 _078_ (
    n78,
    n2,
    _008_
  );
  nand_1 _079_ (
    n80,
    _005_,
    _009_
  );
  nand_1 _080_ (
    _008_,
    _009_,
    _010_
  );
  nand_1 _081_ (
    n18,
    _010_,
    _011_
  );
  or_1 _082_ (
    n2,
    n75,
    _012_
  );
  nand_1 _083_ (
    n2,
    _007_,
    _013_
  );
  and_1 _084_ (
    _012_,
    _013_,
    _014_
  );
  or_1 _085_ (
    n18,
    _014_,
    _015_
  );
  nand_1 _086_ (
    _011_,
    _015_,
    _016_
  );
  or_1 _087_ (
    n67,
    n75,
    _017_
  );
  nand_1 _088_ (
    n67,
    _007_,
    _018_
  );
  and_1 _089_ (
    _017_,
    _018_,
    _019_
  );
  or_1 _090_ (
    n22,
    _019_,
    _020_
  );
  not_1 _091_ (
    _020_,
    _021_
  );
  or_1 _092_ (
    n12,
    _020_,
    _022_
  );
  nand_1 _093_ (
    n78,
    n67,
    _023_
  );
  nand_1 _094_ (
    n80,
    _006_,
    _024_
  );
  nand_1 _095_ (
    _023_,
    _024_,
    _025_
  );
  nand_1 _096_ (
    n22,
    _025_,
    _026_
  );
  nor_1 _097_ (
    _003_,
    n12,
    _027_
  );
  nand_1 _098_ (
    _026_,
    _027_,
    _028_
  );
  nand_1 _099_ (
    _022_,
    _028_,
    _029_
  );
  nand_1 _100_ (
    _016_,
    _029_,
    _030_
  );
  or_1 _101_ (
    _016_,
    _029_,
    _031_
  );
  and_1 _102_ (
    _030_,
    _031_,
    n42
  );
  nand_1 _103_ (
    n4,
    n78,
    _032_
  );
  nand_1 _104_ (
    _002_,
    n80,
    _033_
  );
  nand_1 _105_ (
    _032_,
    _033_,
    _034_
  );
  nand_1 _106_ (
    n35,
    _034_,
    _035_
  );
  or_1 _107_ (
    n4,
    n75,
    _036_
  );
  nand_1 _108_ (
    n4,
    _007_,
    _037_
  );
  and_1 _109_ (
    _036_,
    _037_,
    _038_
  );
  or_1 _110_ (
    n35,
    _038_,
    _039_
  );
  and_1 _111_ (
    _035_,
    _039_,
    _040_
  );
  or_1 _112_ (
    n57,
    n75,
    _041_
  );
  nand_1 _113_ (
    n57,
    _007_,
    _042_
  );
  and_1 _114_ (
    _041_,
    _042_,
    _043_
  );
  or_1 _115_ (
    n34,
    _043_,
    _044_
  );
  not_1 _116_ (
    _044_,
    _045_
  );
  or_1 _117_ (
    n12,
    _044_,
    _046_
  );
  nand_1 _118_ (
    n78,
    n57,
    _047_
  );
  nand_1 _119_ (
    n80,
    _004_,
    _048_
  );
  nand_1 _120_ (
    _047_,
    _048_,
    _049_
  );
  nand_1 _121_ (
    n34,
    _049_,
    _050_
  );
  or_1 _122_ (
    n12,
    _015_,
    _051_
  );
  nand_1 _123_ (
    _011_,
    _029_,
    _052_
  );
  nand_1 _124_ (
    _051_,
    _052_,
    _053_
  );
  nand_1 _125_ (
    _050_,
    _053_,
    _054_
  );
  and_1 _126_ (
    _046_,
    _054_,
    _055_
  );
  nand_1 _127_ (
    _040_,
    _055_,
    _056_
  );
  or_1 _128_ (
    _040_,
    _055_,
    _057_
  );
  and_1 _129_ (
    _056_,
    _057_,
    n65
  );
  nand_1 _130_ (
    _044_,
    _050_,
    _058_
  );
  nand_1 _131_ (
    _053_,
    _058_,
    _059_
  );
  or_1 _132_ (
    _053_,
    _058_,
    _060_
  );
  and_1 _133_ (
    _059_,
    _060_,
    n9
  );
  and_1 _134_ (
    _035_,
    _050_,
    _061_
  );
  and_1 _135_ (
    _011_,
    _026_,
    _062_
  );
  nand_1 _136_ (
    _061_,
    _062_,
    n77
  );
  or_1 _137_ (
    _003_,
    n77,
    _063_
  );
  nand_1 _138_ (
    _035_,
    _045_,
    _064_
  );
  and_1 _139_ (
    _039_,
    _064_,
    _065_
  );
  nand_1 _140_ (
    _011_,
    _021_,
    _066_
  );
  nand_1 _141_ (
    _015_,
    _066_,
    _067_
  );
  nand_1 _142_ (
    _061_,
    _067_,
    _068_
  );
  and_1 _143_ (
    _065_,
    _068_,
    n48
  );
  nand_1 _144_ (
    _063_,
    n48,
    n68
  );
  and_1 _145_ (
    _020_,
    _026_,
    _069_
  );
  or_1 _146_ (
    _027_,
    _069_,
    _070_
  );
  nand_1 _147_ (
    _027_,
    _069_,
    _071_
  );
  nand_1 _148_ (
    _070_,
    _071_,
    n6
  );
  and_1 _149_ (
    n42,
    n6,
    _000_
  );
  and_1 _150_ (
    n9,
    _000_,
    _001_
  );
  and_1 _151_ (
    n65,
    _001_,
    n56
  );
endmodule